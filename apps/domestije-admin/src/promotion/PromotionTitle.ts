import { Promotion as TPromotion } from "../api/promotion/Promotion";

export const PROMOTION_TITLE_FIELD = "id";

export const PromotionTitle = (record: TPromotion): string => {
  return record.id?.toString() || String(record.id);
};
