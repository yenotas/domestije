import { CategoryListRelationFilter } from "../category/CategoryListRelationFilter";
import { FloatNullableFilter } from "../../util/FloatNullableFilter";
import { StringFilter } from "../../util/StringFilter";
import { ProductListRelationFilter } from "../product/ProductListRelationFilter";
import { UserWhereUniqueInput } from "../user/UserWhereUniqueInput";

export type PromotionWhereInput = {
  categories?: CategoryListRelationFilter;
  discountPercent?: FloatNullableFilter;
  id?: StringFilter;
  products?: ProductListRelationFilter;
  user?: UserWhereUniqueInput;
};
