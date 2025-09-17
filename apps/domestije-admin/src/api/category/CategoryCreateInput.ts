import { ProductCreateNestedManyWithoutCategoriesInput } from "./ProductCreateNestedManyWithoutCategoriesInput";
import { PromotionWhereUniqueInput } from "../promotion/PromotionWhereUniqueInput";
import { SliderCreateNestedManyWithoutCategoriesInput } from "./SliderCreateNestedManyWithoutCategoriesInput";

export type CategoryCreateInput = {
  descriptionEn?: string | null;
  descriptionRs?: string | null;
  descriptionRu?: string | null;
  parent?: string | null;
  products?: ProductCreateNestedManyWithoutCategoriesInput;
  promotion?: PromotionWhereUniqueInput | null;
  sliders?: SliderCreateNestedManyWithoutCategoriesInput;
  titleEn?: string | null;
  titleRs?: string | null;
  titleRu?: string | null;
};
