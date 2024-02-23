export interface Language {
  symbold: string;
  originalName: string;
  englishName: string;
}

export interface UnitOptions {
  unitName: string;
  unitTicker: string;
  unitDescription: string;
  unitSrc: string;
  unitId: number;
  languages: Language[];
}
