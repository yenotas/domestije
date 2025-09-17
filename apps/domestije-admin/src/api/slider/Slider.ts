import { Category } from "../category/Category";
import { Product } from "../product/Product";

export type Slider = {
  category?: Category | null;
  createdAt: Date;
  id: string;
  imageUrl: string | null;
  linkType?: "Product" | "Category" | "External" | null;
  product?: Product | null;
  subtitleEn: string | null;
  subtitleRs: string | null;
  subtitleRu: string | null;
  titleEn: string | null;
  titleRs: string | null;
  titleRu: string | null;
  updatedAt: Date;
  videoUrl: string | null;
};
