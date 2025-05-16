import * as React from "react";
import {
  Edit,
  SimpleForm,
  EditProps,
  ReferenceInput,
  SelectInput,
  TextInput,
} from "react-admin";
import { CategoryTitle } from "../category/CategoryTitle";
import { ProductTitle } from "../product/ProductTitle";

export const SliderEdit = (props: EditProps): React.ReactElement => {
  return (
    <Edit {...props}>
      <SimpleForm>
        <ReferenceInput
          source="category.id"
          reference="Category"
          label="category"
        >
          <SelectInput optionText={CategoryTitle} />
        </ReferenceInput>
        <TextInput label="image_url" source="imageUrl" />
        <SelectInput
          source="linkType"
          label="link_type"
          choices={[
            { label: "product ", value: "Product" },
            { label: "category", value: "Category" },
            { label: "external ", value: "External" },
          ]}
          optionText="label"
          allowEmpty
          optionValue="value"
        />
        <ReferenceInput source="product.id" reference="Product" label="product">
          <SelectInput optionText={ProductTitle} />
        </ReferenceInput>
        <TextInput label="subtitle_en" source="subtitleEn" />
        <TextInput label="subtitle_rs" source="subtitleRs" />
        <TextInput label="subtitle_ru" source="subtitleRu" />
        <TextInput label="title_en" source="titleEn" />
        <TextInput label="title_rs" source="titleRs" />
        <TextInput label="title_ru" source="titleRu" />
        <TextInput label="video_url" source="videoUrl" />
      </SimpleForm>
    </Edit>
  );
};
