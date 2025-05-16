import * as graphql from "@nestjs/graphql";
import { SliderResolverBase } from "./base/slider.resolver.base";
import { Slider } from "./base/Slider";
import { SliderService } from "./slider.service";

@graphql.Resolver(() => Slider)
export class SliderResolver extends SliderResolverBase {
  constructor(protected readonly service: SliderService) {
    super(service);
  }
}
