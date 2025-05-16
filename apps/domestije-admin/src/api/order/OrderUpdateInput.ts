import { ProductWhereUniqueInput } from "../product/ProductWhereUniqueInput";
import { UserWhereUniqueInput } from "../user/UserWhereUniqueInput";

export type OrderUpdateInput = {
  product?: ProductWhereUniqueInput | null;
  status?: "Processing" | "New" | "Completed" | "Cancelled" | null;
  user?: UserWhereUniqueInput | null;
};
