import * as React from "react";
import {
  List,
  Datagrid,
  ListProps,
  DateField,
  TextField,
  BooleanField,
} from "react-admin";
import Pagination from "../Components/Pagination";

export const ProductList = (props: ListProps): React.ReactElement => {
  return (
    <List
      {...props}
      title={"Products"}
      perPage={50}
      pagination={<Pagination />}
    >
      <Datagrid rowClick="show" bulkActionButtons={false}>
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
        <DateField source="updatedAt" label="Updated At" />{" "}
      </Datagrid>
    </List>
  );
};
