import {BASE_API_PATH} from "../consts";
import {
    AlgoRequestI,
    AllAlgosRequestT,
} from "../types /types";

export function getAllDatasets(): Promise<AllAlgosRequestT> {
    return fetch(`${BASE_API_PATH}/all_algos`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(resp => resp.json())
        .catch(err => console.error(err));
}


export function getAlgo(algo: string): Promise<AlgoRequestI> {
    return fetch(`${BASE_API_PATH}/get_algo_params1?algo=${algo}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(resp => resp.json())
        .catch(err => console.error(err));
}

export function executeAlgo(
    algo: string,
    params: {
        trade_strategy: undefined | string;
        interval: undefined | string;
        pred_shift: undefined | string;
        features_dict_size: undefined | string;
        models_size: undefined | string;
    }
): Promise<number[]> {
    return fetch(`${BASE_API_PATH}/execute_algo?algo=${algo}&trade_strategy=${params.trade_strategy}&interval=${params.interval}&pred_shift=${params.pred_shift}&features_dict_size=${params.features_dict_size}&models_size=${params.models_size}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(resp => resp.json())
        .catch(err => console.error(err));
}
