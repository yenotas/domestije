import { CategoryUpdateManyWithoutProductsInput } from "./CategoryUpdateManyWithoutProductsInput";
import { OrderUpdateManyWithoutProductsInput } from "./OrderUpdateManyWithoutProductsInput";
import { ProductImageUpdateManyWithoutProductsInput } from "./ProductImageUpdateManyWithoutProductsInput";
import { PromotionUpdateManyWithoutProductsInput } from "./PromotionUpdateManyWithoutProductsInput";
import { SliderUpdateManyWithoutProductsInput } from "./SliderUpdateManyWithoutProductsInput";

export type ProductUpdateInput = {
  category?: CategoryUpdateManyWithoutProductsInput;
  descriptionEn?: string | null;
  descriptionRs?: string | null;
  descriptionRu?: string | null;
  isActive?: boolean | null;
  orders?: OrderUpdateManyWithoutProductsInput;
  price?: number | null;
  productImages?: ProductImageUpdateManyWithoutProductsInput;
  promotions?: PromotionUpdateManyWithoutProductsInput;
  sku?: string | null;
  sliders?: SliderUpdateManyWithoutProductsInput;
  titleEn?: string | null;
  titleRs?: string | null;
  titleRu?: string | null;
};
