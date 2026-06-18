import pickle
import pandas as pd
import numpy as np
import casadi as cd
import subprocess
from pathlib import Path
import time
import datetime
import os, pickle

#from rl_mpc_agents import RL_MPC_GA_agent
from rl_mpc_agents_stoch import RL_MPC_SPG_REINFORCE_agent as Agent

from surrogate_mpc import get_mpc
from collections import deque


from openopc2.config import OpenOpcConfig
from openopc2.utils import get_opc_da_client

#from asyncua import Client, ua
import statistics
import msvcrt



class BatchColumn:
    def __init__(self):
        """
        Let the config as it is
        Use Network 4 on Computer, IP tested is 192.168.10.69
        Install openopc2, disable Fireewall and the script should be working, when WinCC Computer is on (Maybe start "OPC Scout" manually on OS-ServerBK and activate WinCCServer)
        Check this file for all available functions of OPC client C:\ProgramData\miniforge3\envs\opc\Lib\site-packages\openopc2\da_client.py
        """
        open_opc_config = OpenOpcConfig()
        open_opc_config.OPC_SERVER = "OPCServer.WinCC.1"
        open_opc_config.OPC_GATEWAY_HOST = "192.168.10.5"
        open_opc_config.OPC_CLASS = "Graybox.OPC.DAWrapper"
        open_opc_config.OPC_MODE = 'gateway'
        self.opc_client = get_opc_da_client(open_opc_config)
        if self.opc_client.ping() is False:
            print("OPC client lost connection")


        print("Loading MPC agent")
        path_to_agent = "untrained_agent_260508"
        path_to_rl_parameters = "untrained_agent_260508"
        path_to_hyperparameters = "untrained_agent_260508\hyperparams.pkl"
#        self.agent = RL_MPC_GA_agent.load(path_to_agent, load_differentiator=False)
        self.agent = Agent.load(path_to_agent, load_differentiator=False)
        self.agent.load_rl_parameters(path_to_rl_parameters)
        with open(path_to_hyperparameters, "rb") as f:
            self.mpc_hyperparameters = pickle.load(f)



        # model_path = os.path.join("models", "251118_Sampling1000T_PE35", "narx_8step_v1")
        # with open(os.path.join(model_path, "do_mpc_model.pkl"), "rb") as f:
        #     do_mpc_model = pickle.load(f)
            
        # self.mpc = get_mpc(do_mpc_model, hard_constraint=False)
        # self.mpc.setup()
        # self.mpc.reset_history()

        self.data_x = deque(maxlen=self.mpc_hyperparameters.total_number_of_steps)
        self.data_u = deque(maxlen=self.mpc_hyperparameters.total_number_of_steps)
        self.rawdata_x = []
        self.alldata_x = []
        self.alldata_u = []

        self.timestep = self.agent.mpc.settings.t_step
        
        self.sensornames = ['x_e0_LI', 'x_e0_WI', 'x_e0_w_L_D_c1', 'x_e0_w_L_B_c1', 'x_e0_T_tr9'] 

        self.controlnames = ['u_rr', 'u_Q']
        self.sensordict = {
                            'x_e0_LI': 'SensorMeans/LI02_mean.PV#Value',
                            'x_e0_WI': 'Refraktometer/WI01.PV#Value',
                            'x_e0_w_L_B_c1': 'Refraktometer/QI02_SS.PV#Value',
                            'x_e0_w_L_D_c1': 'Refraktometer/QI01_w12.PV#Value',
                            'x_e0_T_tr9': 'SensorMeans/TI12_mean.PV#Value',
                            }
        self.controldict = {
                            'u_rr': 'Reflux/Inp_Refluxratio.SP_Int',
                            'u_Q': 'AnalogOut/Soll-Wert-Heizun.SP_Int',
                            }

        self._emacounter = None
        self._ema_steps = None


    def _receive_states(self):
        datum = np.empty(shape=(len(self.sensornames)))
        for i, sensor in enumerate(self.sensornames):
            if "e0_w_" in sensor:
                value = self.opc_client.read(self.sensordict[sensor])[0]/100
            elif "e0_T_" in sensor:
                value = self.opc_client.read(self.sensordict[sensor])[0]+273
            elif "e0_LI" in sensor:
                value = self.opc_client.read(self.sensordict[sensor])[0] + 7
            else:
                value = self.opc_client.read(self.sensordict[sensor])[0]
            datum[i] = value
        return datum
    
    def _receive_controls(self):
        datum = np.empty(shape=(len(self.controlnames)))
        for i, control in enumerate(self.controlnames):
            if "u_rr" in control:
                value = self.opc_client.read(self.controldict[control])[0]/100
            elif "u_Q" in control:
                value = self.opc_client.read(self.controldict[control])[0]/1000
            datum[i] = value
        return datum

    def update_states(self, ema=True):
        datum = self._receive_states()
        ema_datum = self._apply_ema(datum.reshape(-1,1), bias_correct=False).flatten() if ema else datum
        self.data_x.append(ema_datum.reshape(-1,1))
        self.alldata_x.append(ema_datum.reshape(-1,1).copy())
        if ema:
            self.rawdata_x.append(datum.reshape(-1,1).copy())

    def update_controls(self):
        controls = self._receive_controls()
        self.data_u.append(np.array(controls).reshape(-1,1))
        self.alldata_u.append(np.array(controls).reshape(-1,1).copy())

    def _transmit_controls(self, controls):
        """
        Transmits control values to OPC-UA server
        controls: list or array of control values in order of self.controlnames
        """
        try:
            self.opc_client.write(("Reflux/Inp_Refluxratio.SP_Int", float(controls[0])*100))
            self.opc_client.write(("AnalogOut/Soll-Wert-Heizun.SP_Int",float(controls[1])*1000))
            return True
        except Exception as e:
            print(f"Error transmitting controls: {e}")
            return False
        
    def _get_current_state(self):
        """
        Returns the current state as a casadi DM object
        """
        if len(self.data_x) == 0:
            raise ValueError("No data available to get current state")
        current_state = cd.DM(self.data_x[-1])
        return current_state

    def _apply_ema(self, current_measurement, bias_correct=False):
        """
        Apply exponential moving average (EMA) to a (5,1) measurement,
        with optional bias correction.

        Parameters
        ----------
        current_measurement : ndarray shape (5,1)
            Current measurement vector.
        bias_correct : bool
            Whether to apply EMA bias correction.

        Returns
        -------
        ndarray shape (5,1)
            Smoothed value.
        """
        # Per-dimension alpha values
#        alpha = np.asarray([0.3, 0.3, 0.1, 0.1, 0.1], dtype=float).reshape(5, 1)
#        alpha = np.asarray([0.3, 0.3, 0.3, 0.3, 0.3], dtype=float).reshape(5, 1)
        alpha = np.asarray([0.4, 0.4, 0.4, 0.4, 0.4], dtype=float).reshape(5, 1)

        x = current_measurement.astype(float)

        # Initialize state on first call
        if self._emacounter is None:
            self._emacounter = x.copy()
            self._ema_steps = np.ones((5, 1), dtype=int)
            return x.copy()

        if np.any(self._ema_steps <= 1):
            y = x.copy()
            self._emacounter = y
            self._ema_steps += 1  # Increment before computing
            return y

        # Update EMA
        self._ema_steps += 1
        prev = self._emacounter
        y = alpha * x + (1.0 - alpha) * prev
        self._emacounter = y

        if bias_correct and np.any(self._ema_steps > 5):
            # Compute bias correction factor: 1 - (1-alpha)^t
            correction = 1.0 - np.power(1.0 - alpha, self._ema_steps)
            correction = np.maximum(correction, 1e-10)  # Avoid division by zero
            y = y / correction

        return y

    def _get_user_input(self, str, timeout):
        print(str, flush=True)
        start_time = time.time()
        while time.time()-start_time < timeout:
            if msvcrt.kbhit():
                char = msvcrt.getwch()
                if char == 'y':
                    return 'y'
                else:
                    return ''
            time.sleep(0.1)
        return ''
    
    def _valve_check_loop(self):  # This Function is called if the input during a valve check was wrong
        while True:
            print('Wir versuchen nochmal die y-Taste zu finden.')
            inputcheck = input('Wenn das Ventil betaetigt wurde, bitte "y" eingeben: ')
            if inputcheck == 'y':
                return True

    def startup(self, pump_ramp_parameter=50, desired_level=50, heater_ramp_parameter=2000, max_duty=6000, recipe_qduty=5000, phase=0):
        print('start up process of column initiated.')
        done = False
        data_TI17_len = 3
        data_TI17 = deque(maxlen=data_TI17_len)

        while not done:
            it_start = time.time()
            self.update_states()
            # print('N2 is needed to fill the column for inertisation.')
            # inputcheck = input('Das Ventil XXX muss jetzt manuell geoeffnet werden. Wenn dies erfolgt ist, bitte mit "y" im Terminal bestaetigen: ')
            # while not inputcheck :
            #     inputcheck = self.Valve_Check_Loop()
            if phase == 0:
                print(f'STARTUP PHASE {phase}: Inertisierung')
                inp = self._get_user_input("Inertisierung und V11/V12 mit (y) bestätigen", self.timestep-1)
                if inp == 'y':
                    print('ok')
                    phase += 1
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue
            
            if phase == 1:
                print(f'STARTUP PHASE {phase}: Start to fill reboiler')
                self.opc_client.write(("DigitalOut/Pumpe$Ein-Aus.SetOp",True))    # Einschalten der Pumpe
                phase+=1

            if phase == 2:
                print(f'STARTUP PHASE {phase}: pump ramp')
                curr_npump = self.opc_client.read("AnalogOut/Drehzahl$Pumpe.SP_Int")[0]
                if curr_npump <= 100:    # Rampe um den Feedstrom anzufahren
                    new_npump = min(100,curr_npump+pump_ramp_parameter)
                    self.opc_client.write(("AnalogOut/Drehzahl$Pumpe.SP_Int", new_npump))
                    if new_npump == 100:
                        phase += 1
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue

            if phase == 3:
                print(f'STARTUP PHASE {phase}: wait until full')
                curr_lvl = self.opc_client.read("SensorMeans/LI02_mean.PV#Value")[0]
                print(f'{curr_lvl=}')
                if curr_lvl >= desired_level:
                    self.opc_client.write(("AnalogOut/Drehzahl$Pumpe.SP_Int", 0))
                    self.opc_client.write(("DigitalOut/Pumpe$Ein-Aus.RstOp", True))
                    print('stopped')
                    phase += 1
                self.update_controls()
                #time.sleep(max(0,self.timestep-time.time()+it_start))
                time.sleep(1)
                continue

            if phase == 4:
                print(f'STARTUP PHASE {phase}: V11/V12')
                inp = self._get_user_input("V11/V12 umschalten und mit (y) bestätigen", self.timestep-1)
                if inp == 'y':
                    print('ok')
                    phase += 1
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue

            if phase == 5:
                print(f'STARTUP PHASE {phase}: switch duty')
                self.opc_client.write(("DigitalOut/Heizkerze$Ein-Au.SetOp",True))
                phase+=1
                continue

            if phase == 6:
                print('ramp heater')
                curr_qduty = self.opc_client.read("AnalogOut/Soll-Wert-Heizun.SP_Int")[0]
                print(f'{curr_qduty=}')
                print(f'{heater_ramp_parameter=}')
                if curr_qduty <= max_duty:    # Rampe um den Feedstrom anzufahren
                    new_qduty = min(max_duty,curr_qduty+heater_ramp_parameter)
                    print(f'{new_qduty=}')
                    self.opc_client.write(("AnalogOut/Soll-Wert-Heizun.SP_Int", new_qduty))

                    if new_qduty == max_duty:
                        phase += 1
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue                
            
            if phase == 7:
                print(f'STARTUP PHASE {phase}: wait for T12 > 85degC and reset heatduty')
                curr_temp = self.opc_client.read("SensorMeans/TI12_mean.PV#Value")[0]
                data_TI17.append(self.opc_client.read("SensorMeans/TI17_mean.PV#Value")[0])
                print(f'{curr_temp=}')
                if curr_temp >= 85:
                    self.opc_client.write(("AnalogOut/Soll-Wert-Heizun.SP_Int",recipe_qduty))
                    phase += 1
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue
            
            if phase == 8:
                print(f'STARTUP PHASE {phase}: wait SS')
                curr_T17 = self.opc_client.read("SensorMeans/TI17_mean.PV#Value")[0]
                data_TI17.append(curr_T17)

                curr_temp_std = statistics.stdev(data_TI17) if len(data_TI17) == data_TI17_len else 100.0
                print(f'{curr_temp_std=}')
                print(f'{curr_T17=}')
                print(f'{data_TI17=}')
                if curr_T17 >= 70 and curr_temp_std <= 0.1:
                    phase += 1
                    done = True
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))

    def operation(self, recipe_endtemp=98, target_product_mass = 10e3, max_counter=360, phase=0):
        print('open product valve')
        print('start production')
        done = False
        while not done:
            it_start = time.time()
            self.update_states()

            if phase == 0:
                # NOTE: Add interization here
                print(f'PRODUCTION PHASE {phase}: Handventil, Inertisierung')
                self.opc_client.write(("DigitalOut/VRR_aktiv.SetOp",True))
                inp = self._get_user_input("Handventil Produktabfuhr mit (y) bestätigen", self.timestep-1)
                if inp == 'y':
                    print('ok')
                    phase += 1
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue
            
            if phase == 1:
                print(f'PRODUCTION PHASE {phase}: PRODUCTION')
                self.starttime = time.time()
                operating_time = 0
                
#                u0 = cd.DM(self.data_u[-1])
                u0 = cd.DM(self._receive_controls())
                x0 = cd.DM(np.vstack([*list(self.data_x), *list(self.data_u), operating_time]))
                
                self.agent.mpc.x0.master = x0
                self.agent.mpc.u0.master = u0
                self.agent.mpc.set_initial_guess()

#                u0 = self.agent.act(state = x0, old_action = u0, training = False)
                u0 = self.agent.act(state=x0, old_action=u0, training=False, deterministic=True)["policy_action"]
                
                counter = 0
                phase += 1
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue

            if phase == 2:
                counter += 1
                print(f'--- MPC Iteration {counter} ---')
                product_mass =  self.opc_client.read("Refraktometer/WI01.PV#Value")[0]
                curr_temp = self.opc_client.read("SensorMeans/TI12_mean.PV#Value")[0]
                if product_mass >= target_product_mass or counter >= max_counter or curr_temp >= recipe_endtemp:
                    print('finishing MPC')
                    phase += 1
                    self.update_controls()
                    #time.sleep(max(0,self.timestep-time.time()+it_start))
                    continue

                operating_time = time.time() - self.starttime
                x0 = cd.DM(np.vstack([*list(self.data_x), *list(self.data_u), operating_time]))
                self.agent.mpc.x0.master = x0
                #print(f'____________{x0=}')
                u0 = self.agent.act(state = x0, old_action = self.data_u[-1] if len(self.data_u) > 0 else None, training = False, deterministic=True)["policy_action"].flatten()
                self._transmit_controls(u0)
                print(f"Transmitted controls: {u0}")#\n current state: {self.data_x}")
                self.update_controls()
                time.sleep(max(0,self.timestep-time.time()+it_start))
                continue

            if phase == 3:
                print('shuting down plant')
                self.opc_client.write(("Reflux/Inp_Refluxratio.SP_Int",100))
                self.opc_client.write(("DigitalOut/VRR_aktiv.RstOp",True))
                self.opc_client.write(("AnalogOut/Soll-Wert-Heizun.SP_Int",0))
                self.opc_client.write(("DigitalOut/Heizkerze$Ein-Au.RstOp",True))
                phase += 1
                done = True
                self.update_controls()
                #time.sleep(max(0,self.timestep-time.time()+it_start))
                print('Shutdown, open Nitrogen')


if __name__ == "__main__":
    myCol = BatchColumn()
    # if True:
    #     for i in range(10):
    #         myCol.update_states()
    #         myCol.update_controls()

    myCol.startup(phase=5, desired_level=56, recipe_qduty=5000)
    myCol.operation(phase=0, recipe_endtemp=98, target_product_mass=6000)
    myCol.opc_client.close()
    with open("MPC_RESULT_realplant_untrained_260508.pkl", "wb") as f:
        pickle.dump({'states': myCol.alldata_x, 'controls': myCol.alldata_u, 'rawdata':myCol.rawdata_x}, f)
    myCol.agent.save(r"C:\Users\Administrator\Desktop\251128_MPC\untrained_agent_260508\results\MPC_untrained")
    with open(r"C:\Users\Administrator\Desktop\251128_MPC\untrained_agent_260508\results\trajectories.pkl", "wb") as f:
        pickle.dump(myCol.agent.mpc.data, f)

    print('DONE!!!')