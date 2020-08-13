# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

# Simulation configs, input any new simulations here
from prey_predator_sd import config
# from prey_predator_abm import config
#from {new_simulation} import config

from cadCAD import configs
import pandas as pd


def run(drop_midsteps: bool=True) -> pd.DataFrame:
    """
    Run all experiments and return their output on the dataset column.
    Each line represents an iteration of the parameter-sweep combinations.
    """
    
    exec_mode = ExecutionMode()
    local_mode_ctx = ExecutionContext(context=exec_mode.multi_mode)
    run = Executor(exec_context=local_mode_ctx, configs=configs)
    results = pd.DataFrame()
    i = 0
    for raw_result, _tensor_field, _sessions in run.execute():
        params = configs[i].sim_config['M']
        result_record = pd.DataFrame.from_records([tuple([i for i in params.values()])], columns=list(params.keys()))

        df = pd.DataFrame(raw_result, index=[0])
        # keep only last substep of each timestep
        if drop_midsteps:
            max_substep = max(df.substep)
            is_droppable = (df.substep!=max_substep)&(df.substep!=0)
            df.drop(df[is_droppable].index, inplace=True)

        result_record['dataset'] = [df]
        results = results.append(result_record)
        i += 1
    return results.reset_index()