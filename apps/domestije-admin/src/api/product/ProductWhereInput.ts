import { CategoryListRelationFilter } from "../category/CategoryListRelationFilter";
import { StringNullableFilter } from "../../util/StringNullableFilter";
import { StringFilter } from "../../util/StringFilter";
import { BooleanNullableFilter } from "../../util/BooleanNullableFilter";
import { OrderListRelationFilter } from "../order/OrderListRelationFilter";
import { FloatNullableFilter } from "../../util/FloatNullableFilter";
import { ProductImageListRelationFilter } from "../productImage/ProductImageListRelationFilter";
import { PromotionListRelationFilter } from "../promotion/PromotionListRelationFilter";
import { SliderListRelationFilter } from "../slider/SliderListRelationFilter";

export type ProductWhereInput = {
  category?: CategoryListRelationFilter;
  descriptionEn?: StringNullableFilter;
  descriptionRs?: StringNullableFilter;
  descriptionRu?: StringNullableFilter;
  id?: StringFilter;
  isActive?: BooleanNullableFilter;
  orders?: OrderListRelationFilter;
  price?: FloatNullableFilter;
  productImages?: ProductImageListRelationFilter;
  promotions?: PromotionListRelationFilter;
  sku?: StringNullableFilter;
  sliders?: SliderListRelationFilter;
  titleEn?: StringNullableFilter;
  titleRs?: StringNullableFilter;
  titleRu?: StringNullableFilter;
};
