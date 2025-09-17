import { SliderWhereInput } from "./SliderWhereInput";
import { SliderOrderByInput } from "./SliderOrderByInput";

export type SliderFindManyArgs = {
  where?: SliderWhereInput;
  orderBy?: Array<SliderOrderByInput>;
  skip?: number;
  take?: number;
};
