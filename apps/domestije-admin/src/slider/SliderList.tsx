import * as React from "react";
import {
  List,
  Datagrid,
  ListProps,
  ReferenceField,
  TextField,
  DateField,
} from "react-admin";
import Pagination from "../Components/Pagination";
import { CATEGORY_TITLE_FIELD } from "../category/CategoryTitle";
import { PRODUCT_TITLE_FIELD } from "../product/ProductTitle";

export const SliderList = (props: ListProps): React.ReactElement => {
  return (
    <List {...props} title={"Sliders"} perPage={50} pagination={<Pagination />}>
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
        <TextField label="video_url" source="videoUrl" />{" "}
      </Datagrid>
    </List>
  );
};
