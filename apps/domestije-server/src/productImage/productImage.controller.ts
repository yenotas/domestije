import * as common from "@nestjs/common";
import * as swagger from "@nestjs/swagger";
import { ProductImageService } from "./productImage.service";
import { ProductImageControllerBase } from "./base/productImage.controller.base";

@swagger.ApiTags("productImages")
@common.Controller("productImages")
export class ProductImageController extends ProductImageControllerBase {
  constructor(protected readonly service: ProductImageService) {
    super(service);
  }
}
