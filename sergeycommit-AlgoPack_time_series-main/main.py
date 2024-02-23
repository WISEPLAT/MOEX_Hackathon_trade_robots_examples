from algomodels.model import train
from company_conf import company_configs

if __name__ == '__main__':
    for name in company_configs:
        train(name)