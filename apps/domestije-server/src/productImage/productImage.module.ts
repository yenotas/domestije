import { Module } from "@nestjs/common";
import { ProductImageModuleBase } from "./base/productImage.module.base";
import { ProductImageService } from "./productImage.service";
import { ProductImageController } from "./productImage.controller";
import { ProductImageResolver } from "./productImage.resolver";

@Module({
  imports: [ProductImageModuleBase],
  controllers: [ProductImageController],
  providers: [ProductImageService, ProductImageResolver],
  exports: [ProductImageService],
})
export class ProductImageModule {}
