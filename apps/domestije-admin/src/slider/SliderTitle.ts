import { Slider as TSlider } from "../api/slider/Slider";

export const SLIDER_TITLE_FIELD = "subtitleEn";

export const SliderTitle = (record: TSlider): string => {
  return record.subtitleEn?.toString() || String(record.id);
};
