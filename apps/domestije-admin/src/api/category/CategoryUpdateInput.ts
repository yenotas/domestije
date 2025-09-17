import { ProductUpdateManyWithoutCategoriesInput } from "./ProductUpdateManyWithoutCategoriesInput";
import { PromotionWhereUniqueInput } from "../promotion/PromotionWhereUniqueInput";
import { SliderUpdateManyWithoutCategoriesInput } from "./SliderUpdateManyWithoutCategoriesInput";

export type CategoryUpdateInput = {
  descriptionEn?: string | null;
  descriptionRs?: string | null;
  descriptionRu?: string | null;
  parent?: string | null;
  products?: ProductUpdateManyWithoutCategoriesInput;
  promotion?: PromotionWhereUniqueInput | null;
  sliders?: SliderUpdateManyWithoutCategoriesInput;
  titleEn?: string | null;
  titleRs?: string | null;
  titleRu?: string | null;
};
