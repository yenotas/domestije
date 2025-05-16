import { Injectable } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { SliderServiceBase } from "./base/slider.service.base";

@Injectable()
export class SliderService extends SliderServiceBase {
  constructor(protected readonly prisma: PrismaService) {
    super(prisma);
  }
}
