import { OrderCreateNestedManyWithoutUsersInput } from "./OrderCreateNestedManyWithoutUsersInput";
import { PromotionCreateNestedManyWithoutUsersInput } from "./PromotionCreateNestedManyWithoutUsersInput";
import { InputJsonValue } from "../../types";

export type UserCreateInput = {
  contact?: string | null;
  cookieId?: string | null;
  email?: string | null;
  firstName?: string | null;
  lastName?: string | null;
  orders?: OrderCreateNestedManyWithoutUsersInput;
  password: string;
  promotions?: PromotionCreateNestedManyWithoutUsersInput;
  roles: InputJsonValue;
  username: string;
};
