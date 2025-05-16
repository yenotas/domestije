import * as React from "react";

import {
  Show,
  SimpleShowLayout,
  ShowProps,
  DateField,
  TextField,
  ReferenceField,
  ReferenceManyField,
  Datagrid,
} from "react-admin";

import { PROMOTION_TITLE_FIELD } from "./PromotionTitle";
import { USER_TITLE_FIELD } from "../user/UserTitle";

export const PromotionShow = (props: ShowProps): React.ReactElement => {
  return (
    <Show {...props}>
      <SimpleShowLayout>
        <DateField source="createdAt" label="Created At" />
        <TextField label="discount_percent" source="discountPercent" />
        <TextField label="ID" source="id" />
        <DateField source="updatedAt" label="Updated At" />
        <ReferenceField label="user" source="user.id" reference="User">
          <TextField source={USER_TITLE_FIELD} />
        </ReferenceField>
        <ReferenceManyField
          reference="Category"
          target="promotionId"
          label="Categories"
        >
          <Datagrid rowClick="show" bulkActionButtons={false}>
            <DateField source="createdAt" label="Created At" />
            <TextField label="description_en" source="descriptionEn" />
            <TextField label="description_rs" source="descriptionRs" />
            <TextField label="description_ru" source="descriptionRu" />
            <TextField label="ID" source="id" />
            <TextField label="parent" source="parent" />
            <ReferenceField
              label="Promotion"
              source="promotion.id"
              reference="Promotion"
            >
              <TextField source={PROMOTION_TITLE_FIELD} />
            </ReferenceField>
            <TextField label="title_en" source="titleEn" />
            <TextField label="title_rs" source="titleRs" />
            <TextField label="title_ru" source="titleRu" />
            <DateField source="updatedAt" label="Updated At" />
          </Datagrid>
        </ReferenceManyField>
      </SimpleShowLayout>
    </Show>
  );
};
