import { CategoryCreateNestedManyWithoutPromotionsInput } from "./CategoryCreateNestedManyWithoutPromotionsInput";
import { ProductCreateNestedManyWithoutPromotionsInput } from "./ProductCreateNestedManyWithoutPromotionsInput";
import { UserWhereUniqueInput } from "../user/UserWhereUniqueInput";

export type PromotionCreateInput = {
  categories?: CategoryCreateNestedManyWithoutPromotionsInput;
  discountPercent?: number | null;
  products?: ProductCreateNestedManyWithoutPromotionsInput;
  user?: UserWhereUniqueInput | null;
};
