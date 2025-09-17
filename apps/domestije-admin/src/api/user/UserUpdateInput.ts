import { OrderUpdateManyWithoutUsersInput } from "./OrderUpdateManyWithoutUsersInput";
import { PromotionUpdateManyWithoutUsersInput } from "./PromotionUpdateManyWithoutUsersInput";
import { InputJsonValue } from "../../types";

export type UserUpdateInput = {
  contact?: string | null;
  cookieId?: string | null;
  email?: string | null;
  firstName?: string | null;
  lastName?: string | null;
  orders?: OrderUpdateManyWithoutUsersInput;
  password?: string;
  promotions?: PromotionUpdateManyWithoutUsersInput;
  roles?: InputJsonValue;
  username?: string;
};
