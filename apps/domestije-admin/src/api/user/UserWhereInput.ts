import { StringNullableFilter } from "../../util/StringNullableFilter";
import { StringFilter } from "../../util/StringFilter";
import { OrderListRelationFilter } from "../order/OrderListRelationFilter";
import { PromotionListRelationFilter } from "../promotion/PromotionListRelationFilter";

export type UserWhereInput = {
  contact?: StringNullableFilter;
  cookieId?: StringNullableFilter;
  email?: StringNullableFilter;
  firstName?: StringNullableFilter;
  id?: StringFilter;
  lastName?: StringNullableFilter;
  orders?: OrderListRelationFilter;
  promotions?: PromotionListRelationFilter;
  username?: StringFilter;
};
