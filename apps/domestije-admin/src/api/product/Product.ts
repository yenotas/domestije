import { Category } from "../category/Category";
import { Order } from "../order/Order";
import { ProductImage } from "../productImage/ProductImage";
import { Promotion } from "../promotion/Promotion";
import { Slider } from "../slider/Slider";

export type Product = {
  category?: Array<Category>;
  createdAt: Date;
  descriptionEn: string | null;
  descriptionRs: string | null;
  descriptionRu: string | null;
  id: string;
  isActive: boolean | null;
  orders?: Array<Order>;
  price: number | null;
  productImages?: Array<ProductImage>;
  promotions?: Array<Promotion>;
  sku: string | null;
  sliders?: Array<Slider>;
  titleEn: string | null;
  titleRs: string | null;
  titleRu: string | null;
  updatedAt: Date;
};
