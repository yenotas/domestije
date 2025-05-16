import * as graphql from "@nestjs/graphql";
import { PromotionResolverBase } from "./base/promotion.resolver.base";
import { Promotion } from "./base/Promotion";
import { PromotionService } from "./promotion.service";

@graphql.Resolver(() => Promotion)
export class PromotionResolver extends PromotionResolverBase {
  constructor(protected readonly service: PromotionService) {
    super(service);
  }
}
