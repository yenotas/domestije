import * as React from "react";

import {
  Show,
  SimpleShowLayout,
  ShowProps,
  DateField,
  TextField,
  BooleanField,
  ReferenceManyField,
  Datagrid,
  ReferenceField,
} from "react-admin";

import { PRODUCT_TITLE_FIELD } from "./ProductTitle";
import { USER_TITLE_FIELD } from "../user/UserTitle";
import { CATEGORY_TITLE_FIELD } from "../category/CategoryTitle";

export const ProductShow = (props: ShowProps): React.ReactElement => {
  return (
    <Show {...props}>
      <SimpleShowLayout>
        <DateField source="createdAt" label="Created At" />
        <TextField label="description_en" source="descriptionEn" />
        <TextField label="description_rs" source="descriptionRs" />
        <TextField label="description_ru" source="descriptionRu" />
        <TextField label="ID" source="id" />
        <BooleanField label="is_active" source="isActive" />
        <TextField label="price" source="price" />
        <TextField label="sku" source="sku" />
        <TextField label="title_en" source="titleEn" />
        <TextField label="title_rs" source="titleRs" />
        <TextField label="title_ru" source="titleRu" />
        <DateField source="updatedAt" label="Updated At" />
        <ReferenceManyField reference="Order" target="productId" label="Orders">
          <Datagrid rowClick="show" bulkActionButtons={false}>
            <DateField source="createdAt" label="Created At" />
            <TextField label="ID" source="id" />
            <ReferenceField
              label="product"
              source="product.id"
              reference="Product"
            >
              <TextField source={PRODUCT_TITLE_FIELD} />
            </ReferenceField>
            <TextField label="status" source="status" />
            <DateField source="updatedAt" label="Updated At" />
            <ReferenceField label="user" source="user.id" reference="User">
              <TextField source={USER_TITLE_FIELD} />
            </ReferenceField>
          </Datagrid>
        </ReferenceManyField>
        <ReferenceManyField
          reference="ProductImage"
          target="productId"
          label="ProductImages"
        >
          <Datagrid rowClick="show" bulkActionButtons={false}>
            <DateField source="createdAt" label="Created At" />
            <TextField label="ID" source="id" />
            <TextField label="image_url" source="imageUrl" />
            <ReferenceField
              label="product"
              source="product.id"
              reference="Product"
            >
              <TextField source={PRODUCT_TITLE_FIELD} />
            </ReferenceField>
            <DateField source="updatedAt" label="Updated At" />
          </Datagrid>
        </ReferenceManyField>
        <ReferenceManyField
          reference="Slider"
          target="productId"
          label="Sliders"
        >
          <Datagrid rowClick="show" bulkActionButtons={false}>
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
            <ReferenceField
              label="product"
              source="product.id"
              reference="Product"
            >
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
          </Datagrid>
        </ReferenceManyField>
      </SimpleShowLayout>
    </Show>
  );
};
