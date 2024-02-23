package ru.goalgomoex.goalgomoex.entitys.dto.task.calcProfit;

import ru.goalgomoex.goalgomoex.entitys.dto.IDTOEntity;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoValueDV;

public class dtoSignal implements IDTOEntity {
    private dtoValueDV<float[]> markup_signals;
    private dtoValueDV<float[]> neural_signals;
    private dtoValueDV<int[]> neural_trends;

    public dtoSignal() {
    }
    public dtoValueDV<float[]> getMarkup_signals() {
        return markup_signals;
    }

    public void setMarkup_signals(dtoValueDV<float[]> markup_signals) {
        this.markup_signals = markup_signals;
    }

    public dtoValueDV<float[]> getNeural_signals() {
        return neural_signals;
    }

    public void setNeural_signals(dtoValueDV<float[]> neural_signals) {
        this.neural_signals = neural_signals;
    }

    public dtoValueDV<int[]> getNeural_trends() {
        return neural_trends;
    }

    public void setNeural_trends(dtoValueDV<int[]> neural_trends) {
        this.neural_trends = neural_trends;
    }
}
