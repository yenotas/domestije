import * as React from "react";

import {
  Edit,
  SimpleForm,
  EditProps,
  ReferenceArrayInput,
  SelectArrayInput,
  TextInput,
  BooleanInput,
  NumberInput,
} from "react-admin";

import { CategoryTitle } from "../category/CategoryTitle";
import { OrderTitle } from "../order/OrderTitle";
import { ProductImageTitle } from "../productImage/ProductImageTitle";
import { PromotionTitle } from "../promotion/PromotionTitle";
import { SliderTitle } from "../slider/SliderTitle";

export const ProductEdit = (props: EditProps): React.ReactElement => {
  return (
    <Edit {...props}>
      <SimpleForm>
        <ReferenceArrayInput source="category" reference="Category">
          <SelectArrayInput
            optionText={CategoryTitle}
            parse={(value: any) => value && value.map((v: any) => ({ id: v }))}
            format={(value: any) => value && value.map((v: any) => v.id)}
          />
        </ReferenceArrayInput>
        <TextInput label="description_en" multiline source="descriptionEn" />
        <TextInput label="description_rs" multiline source="descriptionRs" />
        <TextInput label="description_ru" multiline source="descriptionRu" />
        <BooleanInput label="is_active" source="isActive" />
        <ReferenceArrayInput source="orders" reference="Order">
          <SelectArrayInput
            optionText={OrderTitle}
            parse={(value: any) => value && value.map((v: any) => ({ id: v }))}
            format={(value: any) => value && value.map((v: any) => v.id)}
          />
        </ReferenceArrayInput>
        <NumberInput label="price" source="price" />
        <ReferenceArrayInput source="productImages" reference="ProductImage">
          <SelectArrayInput
            optionText={ProductImageTitle}
            parse={(value: any) => value && value.map((v: any) => ({ id: v }))}
            format={(value: any) => value && value.map((v: any) => v.id)}
          />
        </ReferenceArrayInput>
        <ReferenceArrayInput source="promotions" reference="Promotion">
          <SelectArrayInput
            optionText={PromotionTitle}
            parse={(value: any) => value && value.map((v: any) => ({ id: v }))}
            format={(value: any) => value && value.map((v: any) => v.id)}
          />
        </ReferenceArrayInput>
        <TextInput label="sku" source="sku" />
        <ReferenceArrayInput source="sliders" reference="Slider">
          <SelectArrayInput
            optionText={SliderTitle}
            parse={(value: any) => value && value.map((v: any) => ({ id: v }))}
            format={(value: any) => value && value.map((v: any) => v.id)}
          />
        </ReferenceArrayInput>
        <TextInput label="title_en" source="titleEn" />
        <TextInput label="title_rs" source="titleRs" />
        <TextInput label="title_ru" source="titleRu" />
      </SimpleForm>
    </Edit>
  );
};
