#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_opt_lot_volume(config, usd_rub):
    #Минимальный оптимальный объем лота в долларах, для минимизации издержек за комисиию
    try:
        if config.comission_type == 'percent':
            if config.comission_currency == 'usd':
                opt_lot_volume = 100*config.min_commission_usd/config.commission_by_percent
            elif config.comission_currency == 'rub':
                opt_lot_volume_rub = 100*config.min_commission_rub/config.commission_by_percent
                opt_lot_volume = opt_lot_volume_rub / usd_rub
        elif config.comission_type == 'share':
            if config.comission_currency == 'usd':
                opt_lot_volume = config.average_shape_price_usd*config.min_commission_usd/config.commission_by_share
            elif config.comission_currency == 'rub':
                opt_lot_volume = config.average_shape_price_rub*config.min_commission_rub/(config.commission_by_share*usd_rub)
        
        return opt_lot_volume
    except:
        print("Error get optimum lot volume")
        
        return None

