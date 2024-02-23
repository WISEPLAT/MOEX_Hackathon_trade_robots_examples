package ru.goalgomoex.goalgomoex.entitys.dto.task.calcProfit;

import ru.goalgomoex.goalgomoex.entitys.dto.dtoData;
import ru.goalgomoex.goalgomoex.entitys.dto.task.dtoTaskOut;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoValueDV;

public class dtoTaskOutCalcProfit extends dtoTaskOut {
    private dtoSignal singals_example;
    private dtoValueDV<Float> test_accuracy_score;
    private dtoValueDV<Float> test_roc_auc_score;
    private dtoValueDV<Float> test_precision_score;
    private dtoValueDV<Float> test_recall_score;
    private dtoValueDV<Float> test_f1_score;
    private dtoValueDV<Float> test_log_loss;
    private dtoValueDV<Float> data_std;
    private dtoValueDV<Float> max_risk;
    private dtoValueDV<Float> buy_hold_std;
    private dtoValueDV<Float> buy_hold_sharp;
    private dtoValueDV<Float> ideal_strategy_profit_without_shift;
    private dtoValueDV<Float> ideal_strategy_profit_with_shift;
    private dtoValueDV<Float> ideal_strategy_std_without_shift;
    private dtoValueDV<Float> ideal_strategy_std_with_shift;
    private dtoValueDV<Float> ideal_strategy_sharp_without_shift;
    private dtoValueDV<Float> ideal_strategy_sharp_with_shift;
    private dtoValueDV<Float> ideal_strategy_trade_count_without_shift;
    private dtoValueDV<Float> neural_strategy_profit_without_shift;
    private dtoValueDV<Float> neural_strategy_profit_with_shift;
    private dtoValueDV<Float> neural_strategy_std_with_shift;
    private dtoValueDV<Float> neural_strategy_sharp_without_shift;
    private dtoValueDV<Float> neural_strategy_sharp_with_shift;
    private dtoValueDV<Float> neural_strategy_trade_count_without_shift;
    private dtoValueDV<Float> neural_strategy_trade_count_with_shift;
    private dtoValueDV<dtoData[]> dyn_ideal_trading;
    private dtoValueDV<dtoData[]> dyn_neural_trading;

    public dtoTaskOutCalcProfit(dtoSignal singals_example, dtoValueDV<Float> test_accuracy_score, dtoValueDV<Float> test_roc_auc_score, dtoValueDV<Float> test_precision_score, dtoValueDV<Float> test_recall_score, dtoValueDV<Float> test_f1_score, dtoValueDV<Float> test_log_loss, dtoValueDV<Float> data_std, dtoValueDV<Float> max_risk, dtoValueDV<Float> buy_hold_std, dtoValueDV<Float> buy_hold_sharp, dtoValueDV<Float> ideal_strategy_profit_without_shift, dtoValueDV<Float> ideal_strategy_profit_with_shift, dtoValueDV<Float> ideal_strategy_std_without_shift, dtoValueDV<Float> ideal_strategy_std_with_shift, dtoValueDV<Float> ideal_strategy_sharp_without_shift, dtoValueDV<Float> ideal_strategy_sharp_with_shift, dtoValueDV<Float> ideal_strategy_trade_count_without_shift, dtoValueDV<Float> neural_strategy_profit_without_shift, dtoValueDV<Float> neural_strategy_profit_with_shift, dtoValueDV<Float> neural_strategy_std_with_shift, dtoValueDV<Float> neural_strategy_sharp_without_shift, dtoValueDV<Float> neural_strategy_sharp_with_shift, dtoValueDV<Float> neural_strategy_trade_count_without_shift, dtoValueDV<Float> neural_strategy_trade_count_with_shift, dtoValueDV<dtoData[]> dyn_ideal_trading, dtoValueDV<dtoData[]> dyn_neural_trading) {
        this.singals_example = singals_example;
        this.test_accuracy_score = test_accuracy_score;
        this.test_roc_auc_score = test_roc_auc_score;
        this.test_precision_score = test_precision_score;
        this.test_recall_score = test_recall_score;
        this.test_f1_score = test_f1_score;
        this.test_log_loss = test_log_loss;
        this.data_std = data_std;
        this.max_risk = max_risk;
        this.buy_hold_std = buy_hold_std;
        this.buy_hold_sharp = buy_hold_sharp;
        this.ideal_strategy_profit_without_shift = ideal_strategy_profit_without_shift;
        this.ideal_strategy_profit_with_shift = ideal_strategy_profit_with_shift;
        this.ideal_strategy_std_without_shift = ideal_strategy_std_without_shift;
        this.ideal_strategy_std_with_shift = ideal_strategy_std_with_shift;
        this.ideal_strategy_sharp_without_shift = ideal_strategy_sharp_without_shift;
        this.ideal_strategy_sharp_with_shift = ideal_strategy_sharp_with_shift;
        this.ideal_strategy_trade_count_without_shift = ideal_strategy_trade_count_without_shift;
        this.neural_strategy_profit_without_shift = neural_strategy_profit_without_shift;
        this.neural_strategy_profit_with_shift = neural_strategy_profit_with_shift;
        this.neural_strategy_std_with_shift = neural_strategy_std_with_shift;
        this.neural_strategy_sharp_without_shift = neural_strategy_sharp_without_shift;
        this.neural_strategy_sharp_with_shift = neural_strategy_sharp_with_shift;
        this.neural_strategy_trade_count_without_shift = neural_strategy_trade_count_without_shift;
        this.neural_strategy_trade_count_with_shift = neural_strategy_trade_count_with_shift;
        this.dyn_ideal_trading = dyn_ideal_trading;
        this.dyn_neural_trading = dyn_neural_trading;
    }

    public dtoTaskOutCalcProfit(long task_id, dtoSignal singals_example, dtoValueDV<Float> test_accuracy_score, dtoValueDV<Float> test_roc_auc_score, dtoValueDV<Float> test_precision_score, dtoValueDV<Float> test_recall_score, dtoValueDV<Float> test_f1_score, dtoValueDV<Float> test_log_loss, dtoValueDV<Float> data_std, dtoValueDV<Float> max_risk, dtoValueDV<Float> buy_hold_std, dtoValueDV<Float> buy_hold_sharp, dtoValueDV<Float> ideal_strategy_profit_without_shift, dtoValueDV<Float> ideal_strategy_profit_with_shift, dtoValueDV<Float> ideal_strategy_std_without_shift, dtoValueDV<Float> ideal_strategy_std_with_shift, dtoValueDV<Float> ideal_strategy_sharp_without_shift, dtoValueDV<Float> ideal_strategy_sharp_with_shift, dtoValueDV<Float> ideal_strategy_trade_count_without_shift, dtoValueDV<Float> neural_strategy_profit_without_shift, dtoValueDV<Float> neural_strategy_profit_with_shift, dtoValueDV<Float> neural_strategy_std_with_shift, dtoValueDV<Float> neural_strategy_sharp_without_shift, dtoValueDV<Float> neural_strategy_sharp_with_shift, dtoValueDV<Float> neural_strategy_trade_count_without_shift, dtoValueDV<Float> neural_strategy_trade_count_with_shift, dtoValueDV<dtoData[]> dyn_ideal_trading, dtoValueDV<dtoData[]> dyn_neural_trading) {
        super(task_id);
        this.singals_example = singals_example;
        this.test_accuracy_score = test_accuracy_score;
        this.test_roc_auc_score = test_roc_auc_score;
        this.test_precision_score = test_precision_score;
        this.test_recall_score = test_recall_score;
        this.test_f1_score = test_f1_score;
        this.test_log_loss = test_log_loss;
        this.data_std = data_std;
        this.max_risk = max_risk;
        this.buy_hold_std = buy_hold_std;
        this.buy_hold_sharp = buy_hold_sharp;
        this.ideal_strategy_profit_without_shift = ideal_strategy_profit_without_shift;
        this.ideal_strategy_profit_with_shift = ideal_strategy_profit_with_shift;
        this.ideal_strategy_std_without_shift = ideal_strategy_std_without_shift;
        this.ideal_strategy_std_with_shift = ideal_strategy_std_with_shift;
        this.ideal_strategy_sharp_without_shift = ideal_strategy_sharp_without_shift;
        this.ideal_strategy_sharp_with_shift = ideal_strategy_sharp_with_shift;
        this.ideal_strategy_trade_count_without_shift = ideal_strategy_trade_count_without_shift;
        this.neural_strategy_profit_without_shift = neural_strategy_profit_without_shift;
        this.neural_strategy_profit_with_shift = neural_strategy_profit_with_shift;
        this.neural_strategy_std_with_shift = neural_strategy_std_with_shift;
        this.neural_strategy_sharp_without_shift = neural_strategy_sharp_without_shift;
        this.neural_strategy_sharp_with_shift = neural_strategy_sharp_with_shift;
        this.neural_strategy_trade_count_without_shift = neural_strategy_trade_count_without_shift;
        this.neural_strategy_trade_count_with_shift = neural_strategy_trade_count_with_shift;
        this.dyn_ideal_trading = dyn_ideal_trading;
        this.dyn_neural_trading = dyn_neural_trading;
    }

    public dtoTaskOutCalcProfit() {
    }

    public dtoTaskOutCalcProfit(long task_id) {
        super(task_id);
    }

    public dtoSignal getSingals_example() {
        return singals_example;
    }

    public void setSingals_example(dtoSignal singals_example) {
        this.singals_example = singals_example;
    }

    public dtoValueDV<Float> getTest_accuracy_score() {
        return test_accuracy_score;
    }

    public void setTest_accuracy_score(dtoValueDV<Float> test_accuracy_score) {
        this.test_accuracy_score = test_accuracy_score;
    }

    public dtoValueDV<Float> getTest_roc_auc_score() {
        return test_roc_auc_score;
    }

    public void setTest_roc_auc_score(dtoValueDV<Float> test_roc_auc_score) {
        this.test_roc_auc_score = test_roc_auc_score;
    }

    public dtoValueDV<Float> getTest_precision_score() {
        return test_precision_score;
    }

    public void setTest_precision_score(dtoValueDV<Float> test_precision_score) {
        this.test_precision_score = test_precision_score;
    }

    public dtoValueDV<Float> getTest_recall_score() {
        return test_recall_score;
    }

    public void setTest_recall_score(dtoValueDV<Float> test_recall_score) {
        this.test_recall_score = test_recall_score;
    }

    public dtoValueDV<Float> getTest_f1_score() {
        return test_f1_score;
    }

    public void setTest_f1_score(dtoValueDV<Float> test_f1_score) {
        this.test_f1_score = test_f1_score;
    }

    public dtoValueDV<Float> getTest_log_loss() {
        return test_log_loss;
    }

    public void setTest_log_loss(dtoValueDV<Float> test_log_loss) {
        this.test_log_loss = test_log_loss;
    }

    public dtoValueDV<Float> getData_std() {
        return data_std;
    }

    public void setData_std(dtoValueDV<Float> data_std) {
        this.data_std = data_std;
    }

    public dtoValueDV<Float> getMax_risk() {
        return max_risk;
    }

    public void setMax_risk(dtoValueDV<Float> max_risk) {
        this.max_risk = max_risk;
    }

    public dtoValueDV<Float> getBuy_hold_std() {
        return buy_hold_std;
    }

    public void setBuy_hold_std(dtoValueDV<Float> buy_hold_std) {
        this.buy_hold_std = buy_hold_std;
    }

    public dtoValueDV<Float> getBuy_hold_sharp() {
        return buy_hold_sharp;
    }

    public void setBuy_hold_sharp(dtoValueDV<Float> buy_hold_sharp) {
        this.buy_hold_sharp = buy_hold_sharp;
    }

    public dtoValueDV<Float> getIdeal_strategy_profit_without_shift() {
        return ideal_strategy_profit_without_shift;
    }

    public void setIdeal_strategy_profit_without_shift(dtoValueDV<Float> ideal_strategy_profit_without_shift) {
        this.ideal_strategy_profit_without_shift = ideal_strategy_profit_without_shift;
    }

    public dtoValueDV<Float> getIdeal_strategy_profit_with_shift() {
        return ideal_strategy_profit_with_shift;
    }

    public void setIdeal_strategy_profit_with_shift(dtoValueDV<Float> ideal_strategy_profit_with_shift) {
        this.ideal_strategy_profit_with_shift = ideal_strategy_profit_with_shift;
    }

    public dtoValueDV<Float> getIdeal_strategy_std_without_shift() {
        return ideal_strategy_std_without_shift;
    }

    public void setIdeal_strategy_std_without_shift(dtoValueDV<Float> ideal_strategy_std_without_shift) {
        this.ideal_strategy_std_without_shift = ideal_strategy_std_without_shift;
    }

    public dtoValueDV<Float> getIdeal_strategy_std_with_shift() {
        return ideal_strategy_std_with_shift;
    }

    public void setIdeal_strategy_std_with_shift(dtoValueDV<Float> ideal_strategy_std_with_shift) {
        this.ideal_strategy_std_with_shift = ideal_strategy_std_with_shift;
    }

    public dtoValueDV<Float> getIdeal_strategy_sharp_without_shift() {
        return ideal_strategy_sharp_without_shift;
    }

    public void setIdeal_strategy_sharp_without_shift(dtoValueDV<Float> ideal_strategy_sharp_without_shift) {
        this.ideal_strategy_sharp_without_shift = ideal_strategy_sharp_without_shift;
    }

    public dtoValueDV<Float> getIdeal_strategy_sharp_with_shift() {
        return ideal_strategy_sharp_with_shift;
    }

    public void setIdeal_strategy_sharp_with_shift(dtoValueDV<Float> ideal_strategy_sharp_with_shift) {
        this.ideal_strategy_sharp_with_shift = ideal_strategy_sharp_with_shift;
    }

    public dtoValueDV<Float> getIdeal_strategy_trade_count_without_shift() {
        return ideal_strategy_trade_count_without_shift;
    }

    public void setIdeal_strategy_trade_count_without_shift(dtoValueDV<Float> ideal_strategy_trade_count_without_shift) {
        this.ideal_strategy_trade_count_without_shift = ideal_strategy_trade_count_without_shift;
    }

    public dtoValueDV<Float> getNeural_strategy_profit_without_shift() {
        return neural_strategy_profit_without_shift;
    }

    public void setNeural_strategy_profit_without_shift(dtoValueDV<Float> neural_strategy_profit_without_shift) {
        this.neural_strategy_profit_without_shift = neural_strategy_profit_without_shift;
    }

    public dtoValueDV<Float> getNeural_strategy_profit_with_shift() {
        return neural_strategy_profit_with_shift;
    }

    public void setNeural_strategy_profit_with_shift(dtoValueDV<Float> neural_strategy_profit_with_shift) {
        this.neural_strategy_profit_with_shift = neural_strategy_profit_with_shift;
    }

    public dtoValueDV<Float> getNeural_strategy_std_with_shift() {
        return neural_strategy_std_with_shift;
    }

    public void setNeural_strategy_std_with_shift(dtoValueDV<Float> neural_strategy_std_with_shift) {
        this.neural_strategy_std_with_shift = neural_strategy_std_with_shift;
    }

    public dtoValueDV<Float> getNeural_strategy_sharp_without_shift() {
        return neural_strategy_sharp_without_shift;
    }

    public void setNeural_strategy_sharp_without_shift(dtoValueDV<Float> neural_strategy_sharp_without_shift) {
        this.neural_strategy_sharp_without_shift = neural_strategy_sharp_without_shift;
    }

    public dtoValueDV<Float> getNeural_strategy_sharp_with_shift() {
        return neural_strategy_sharp_with_shift;
    }

    public void setNeural_strategy_sharp_with_shift(dtoValueDV<Float> neural_strategy_sharp_with_shift) {
        this.neural_strategy_sharp_with_shift = neural_strategy_sharp_with_shift;
    }

    public dtoValueDV<Float> getNeural_strategy_trade_count_without_shift() {
        return neural_strategy_trade_count_without_shift;
    }

    public void setNeural_strategy_trade_count_without_shift(dtoValueDV<Float> neural_strategy_trade_count_without_shift) {
        this.neural_strategy_trade_count_without_shift = neural_strategy_trade_count_without_shift;
    }

    public dtoValueDV<Float> getNeural_strategy_trade_count_with_shift() {
        return neural_strategy_trade_count_with_shift;
    }

    public void setNeural_strategy_trade_count_with_shift(dtoValueDV<Float> neural_strategy_trade_count_with_shift) {
        this.neural_strategy_trade_count_with_shift = neural_strategy_trade_count_with_shift;
    }

    public dtoValueDV<dtoData[]> getDyn_ideal_trading() {
        return dyn_ideal_trading;
    }

    public void setDyn_ideal_trading(dtoValueDV<dtoData[]> dyn_ideal_trading) {
        this.dyn_ideal_trading = dyn_ideal_trading;
    }

    public dtoValueDV<dtoData[]> getDyn_neural_trading() {
        return dyn_neural_trading;
    }

    public void setDyn_neural_trading(dtoValueDV<dtoData[]> dyn_neural_trading) {
        this.dyn_neural_trading = dyn_neural_trading;
    }
}
