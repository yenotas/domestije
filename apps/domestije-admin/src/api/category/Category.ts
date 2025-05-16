import { Product } from "../product/Product";
import { Promotion } from "../promotion/Promotion";
import { Slider } from "../slider/Slider";

export type Category = {
  createdAt: Date;
  descriptionEn: string | null;
  descriptionRs: string | null;
  descriptionRu: string | null;
  id: string;
  parent: string | null;
  products?: Array<Product>;
  promotion?: Promotion | null;
  sliders?: Array<Slider>;
  titleEn: string | null;
  titleRs: string | null;
  titleRu: string | null;
  updatedAt: Date;
};
