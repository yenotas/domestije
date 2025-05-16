import { Module } from "@nestjs/common";
import { SliderModuleBase } from "./base/slider.module.base";
import { SliderService } from "./slider.service";
import { SliderController } from "./slider.controller";
import { SliderResolver } from "./slider.resolver";

@Module({
  imports: [SliderModuleBase],
  controllers: [SliderController],
  providers: [SliderService, SliderResolver],
  exports: [SliderService],
})
export class SliderModule {}
