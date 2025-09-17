import { CategoryWhereUniqueInput } from "../category/CategoryWhereUniqueInput";
import { ProductWhereUniqueInput } from "../product/ProductWhereUniqueInput";

export type SliderUpdateInput = {
  category?: CategoryWhereUniqueInput | null;
  imageUrl?: string | null;
  linkType?: "Product" | "Category" | "External" | null;
  product?: ProductWhereUniqueInput | null;
  subtitleEn?: string | null;
  subtitleRs?: string | null;
  subtitleRu?: string | null;
  titleEn?: string | null;
  titleRs?: string | null;
  titleRu?: string | null;
  videoUrl?: string | null;
};
