import * as common from "@nestjs/common";
import * as swagger from "@nestjs/swagger";
import { SliderService } from "./slider.service";
import { SliderControllerBase } from "./base/slider.controller.base";

@swagger.ApiTags("sliders")
@common.Controller("sliders")
export class SliderController extends SliderControllerBase {
  constructor(protected readonly service: SliderService) {
    super(service);
  }
}
