import * as React from "react";
import {
  Show,
  SimpleShowLayout,
  ShowProps,
  ReferenceField,
  TextField,
  DateField,
} from "react-admin";
import { CATEGORY_TITLE_FIELD } from "../category/CategoryTitle";
import { PRODUCT_TITLE_FIELD } from "../product/ProductTitle";

export const SliderShow = (props: ShowProps): React.ReactElement => {
  return (
    <Show {...props}>
      <SimpleShowLayout>
        <ReferenceField
          label="category"
          source="category.id"
          reference="Category"
        >
          <TextField source={CATEGORY_TITLE_FIELD} />
        </ReferenceField>
        <DateField source="createdAt" label="Created At" />
        <TextField label="ID" source="id" />
        <TextField label="image_url" source="imageUrl" />
        <TextField label="link_type" source="linkType" />
        <ReferenceField label="product" source="product.id" reference="Product">
          <TextField source={PRODUCT_TITLE_FIELD} />
        </ReferenceField>
        <TextField label="subtitle_en" source="subtitleEn" />
        <TextField label="subtitle_rs" source="subtitleRs" />
        <TextField label="subtitle_ru" source="subtitleRu" />
        <TextField label="title_en" source="titleEn" />
        <TextField label="title_rs" source="titleRs" />
        <TextField label="title_ru" source="titleRu" />
        <DateField source="updatedAt" label="Updated At" />
        <TextField label="video_url" source="videoUrl" />
      </SimpleShowLayout>
    </Show>
  );
};
