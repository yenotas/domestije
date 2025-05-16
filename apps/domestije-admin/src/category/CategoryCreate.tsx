import * as React from "react";

import {
  Create,
  SimpleForm,
  CreateProps,
  TextInput,
  ReferenceArrayInput,
  SelectArrayInput,
  ReferenceInput,
  SelectInput,
} from "react-admin";

import { ProductTitle } from "../product/ProductTitle";
import { PromotionTitle } from "../promotion/PromotionTitle";
import { SliderTitle } from "../slider/SliderTitle";

export const CategoryCreate = (props: CreateProps): React.ReactElement => {
  return (
    <Create {...props}>
      <SimpleForm>
        <TextInput label="description_en" multiline source="descriptionEn" />
        <TextInput label="description_rs" multiline source="descriptionRs" />
        <TextInput label="description_ru" multiline source="descriptionRu" />
        <TextInput label="parent" source="parent" />
        <ReferenceArrayInput source="products" reference="Product">
          <SelectArrayInput
            optionText={ProductTitle}
            parse={(value: any) => value && value.map((v: any) => ({ id: v }))}
            format={(value: any) => value && value.map((v: any) => v.id)}
          />
        </ReferenceArrayInput>
        <ReferenceInput
          source="promotion.id"
          reference="Promotion"
          label="Promotion"
        >
          <SelectInput optionText={PromotionTitle} />
        </ReferenceInput>
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
    </Create>
  );
};
