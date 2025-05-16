import { CategoryUpdateManyWithoutPromotionsInput } from "./CategoryUpdateManyWithoutPromotionsInput";
import { ProductUpdateManyWithoutPromotionsInput } from "./ProductUpdateManyWithoutPromotionsInput";
import { UserWhereUniqueInput } from "../user/UserWhereUniqueInput";

export type PromotionUpdateInput = {
  categories?: CategoryUpdateManyWithoutPromotionsInput;
  discountPercent?: number | null;
  products?: ProductUpdateManyWithoutPromotionsInput;
  user?: UserWhereUniqueInput | null;
};
