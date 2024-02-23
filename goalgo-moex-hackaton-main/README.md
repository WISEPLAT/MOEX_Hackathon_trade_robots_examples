# goalgo-moex-hackaton
Solutions for https://goalgo.ru/ hackaton

## Link to application
https://goalgo-moex-hackaton-divannye-eksperty.streamlit.app/

### Files description
- `streamlit-langchain-app.py` - main application file
- `strategies.py` - used strategies
- `prophet.py` - alternative implementation of price forecast

## How to run locally (develop mode)
- install dependencies (`requirements.txt` file)
- save secrets toml file to `~/.streamlit/secrets.toml`
- run `python -m streamlit run streamlit-langchain-app.py`

> You can get plots in html file when running strategies only if you run application locally! 
