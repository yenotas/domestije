import { Category } from "../category/Category";
import { Product } from "../product/Product";
import { User } from "../user/User";

export type Promotion = {
  categories?: Array<Category>;
  createdAt: Date;
  discountPercent: number | null;
  id: string;
  products?: Array<Product>;
  updatedAt: Date;
  user?: User | null;
};
