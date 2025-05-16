import { Order } from "../order/Order";
import { Promotion } from "../promotion/Promotion";
import { JsonValue } from "type-fest";

export type User = {
  contact: string | null;
  cookieId: string | null;
  createdAt: Date;
  email: string | null;
  firstName: string | null;
  id: string;
  lastName: string | null;
  orders?: Array<Order>;
  promotions?: Array<Promotion>;
  roles: JsonValue;
  updatedAt: Date;
  username: string;
};
