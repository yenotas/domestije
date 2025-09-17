import { Injectable } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { ProductImageServiceBase } from "./base/productImage.service.base";

@Injectable()
export class ProductImageService extends ProductImageServiceBase {
  constructor(protected readonly prisma: PrismaService) {
    super(prisma);
  }
}
