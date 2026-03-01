// Import for type checking
import {
  checkPluginVersion,
  type InvenTreePluginContext,
  ModelType
} from '@inventreedb/ui';
import { Group, SimpleGrid, Stack, Text, Title } from '@mantine/core';
import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';

/**
 * Render a custom panel with the provided context.
 * Refer to the InvenTree documentation for the context interface
 * https://docs.inventree.org/en/latest/plugins/mixins/ui/#plugin-context
 */
function InvenTreeShipmentDataPanel({
  context
}: {
  context: InvenTreePluginContext;
}) {
  // for sales order pages we want the order ID
  const orderId = useMemo(() => {
    return context.model === ModelType.salesorder ? context.id || null : null;
  }, [context.model, context.id]);

  // fetch shipment data only when viewing a sales order
  const apiQuery = useQuery(
    {
      queryKey: ['soShipmentData', orderId],
      queryFn: async () => {
        if (!orderId) {
          return null;
        }
        const url = `/plugin/inventree-shipment-data/salesorder/${orderId}/shipment-data/`;
        return context.api.get(url).then((response) => response.data);
      },
      enabled: !!orderId
    },
    context.queryClient
  );

  return (
    <Stack gap='xs'>
      <Title c={context.theme.primaryColor} order={3}>
        InvenTree Shipment Data
      </Title>
      {orderId ? (
        apiQuery.isLoading ? (
          <Text>Loading...</Text>
        ) : apiQuery.data ? (
          <Stack gap='xs'>
            <Text>Total weight: {apiQuery.data.total_weight}</Text>
            <Text>Total volume: {apiQuery.data.total_volume}</Text>
            <SimpleGrid cols={1}>
              {apiQuery.data.parts.map((p: any) => (
                <Group key={p.part_id} justify='apart' grow>
                  <Text>{p.part_name ?? '–'}</Text>
                  <Text>qty: {p.quantity}</Text>
                  <Text>wt/ea: {p.weight ?? 'n/a'}</Text>
                  <Text>vol/ea: {p.volume ?? 'n/a'}</Text>
                  <Text>line wt: {p.line_weight}</Text>
                  <Text>line vol: {p.line_volume}</Text>
                </Group>
              ))}
            </SimpleGrid>
          </Stack>
        ) : (
          <Text>No shipment data available</Text>
        )
      ) : (
        <Text>This panel is only available on sales order pages.</Text>
      )}
    </Stack>
  );
}

// This is the function which is called by InvenTree to render the actual panel component
export function renderInvenTreeShipmentDataPanel(
  context: InvenTreePluginContext
) {
  checkPluginVersion(context);

  return <InvenTreeShipmentDataPanel context={context} />;
}
