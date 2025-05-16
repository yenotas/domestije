import { CategoryCreateNestedManyWithoutProductsInput } from "./CategoryCreateNestedManyWithoutProductsInput";
import { OrderCreateNestedManyWithoutProductsInput } from "./OrderCreateNestedManyWithoutProductsInput";
import { ProductImageCreateNestedManyWithoutProductsInput } from "./ProductImageCreateNestedManyWithoutProductsInput";
import { PromotionCreateNestedManyWithoutProductsInput } from "./PromotionCreateNestedManyWithoutProductsInput";
import { SliderCreateNestedManyWithoutProductsInput } from "./SliderCreateNestedManyWithoutProductsInput";

export type ProductCreateInput = {
  category?: CategoryCreateNestedManyWithoutProductsInput;
  descriptionEn?: string | null;
  descriptionRs?: string | null;
  descriptionRu?: string | null;
  isActive?: boolean | null;
  orders?: OrderCreateNestedManyWithoutProductsInput;
  price?: number | null;
  productImages?: ProductImageCreateNestedManyWithoutProductsInput;
  promotions?: PromotionCreateNestedManyWithoutProductsInput;
  sku?: string | null;
  sliders?: SliderCreateNestedManyWithoutProductsInput;
  titleEn?: string | null;
  titleRs?: string | null;
  titleRu?: string | null;
};
