import { en } from "locales/en.locale";
import { ru } from "locales/ru.locale";

type localeType = typeof en | typeof ru;

export function setLocale(locale: string | undefined): localeType {
    switch (locale) {
        case 'ru':
            return ru;
        default:
            return en;
    }
}