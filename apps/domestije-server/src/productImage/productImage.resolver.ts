import * as graphql from "@nestjs/graphql";
import { ProductImageResolverBase } from "./base/productImage.resolver.base";
import { ProductImage } from "./base/ProductImage";
import { ProductImageService } from "./productImage.service";

@graphql.Resolver(() => ProductImage)
export class ProductImageResolver extends ProductImageResolverBase {
  constructor(protected readonly service: ProductImageService) {
    super(service);
  }
}
