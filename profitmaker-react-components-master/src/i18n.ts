import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// the translations
// (tip move them in a JSON file and import them,
// or even better, manage them separated from your code: https://react.i18next.com/guides/multiple-translation-files)
const resources = {
  en: {
    translation: {
      "Description": "Description",
      "Name": "Name",
      "Amount": "Amount",
      "Ticker": "Ticker",
      "From": "From",
      "To": "To",
      "Transaction": "Transaction",
      "Send": "Send",
      "Create": "Create",
      "Save": "Save",
      "Edit": "Edit",
      "Processing": "Processing",
      "Success": "Success",
      "Error": "Error",
      "Cancel": "Cancel",
      "Wallet": "Wallet",
      "Portfolio": "Portfolio",
      "Language": "Language",
      "Languages": "Languages",
      "Add language": "Add language",
      "Remove language": "Remove language",
      "Insert avatar": "Insert avatar",
      "Insert ticker": "Insert ticker",
      "Insert name": "Insert name",
      "Insert description": "Insert description",
      "Search": "Search",
      "Avatar": "Avatar",
    }
  },
  ru: {
    translation: {
      "Description": "Описание",
      "Name": "Имя",
      "Amount": "Количество",
      "Ticker": "Тикер",
      "From": "Откуда",
      "To": "Куда",
      "Transaction": "Транзакция",
      "Send": "Отправить",
      "Create": "Создать",
      "Save": "Сохранить",
      "Edit": "Править",
      "Processing": "Обработка",
      "Success": "Успешно",
      "Error": "Ошибка",
      "Cancel": "Отмена",
      "Wallet": "Кошелек",
      "Portfolio": "Портфель",
      "Language": "Язык",
      "Languages": "Языки",
      "Add language": "Добавить язык",
      "Remove language": "Удалить язык",
      "Insert avatar": "Адрес к аватарке",
      "Insert ticker": "Напишите тикер",
      "Insert name": "Напишите имя",
      "Insert description": "Придумайте описание",
      "Search": "Поиск",
      "Avatar": "Аватарка",
    }
  }
};

i18n
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    resources,
    lng: "ru",
    fallbackLng: "ru",
    interpolation: {
      escapeValue: false // react already safes from xss
    }
  });

  export default i18n;
