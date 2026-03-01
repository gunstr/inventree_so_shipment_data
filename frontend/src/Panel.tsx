// Import for type checking
import {
  checkPluginVersion,
  type InvenTreePluginContext,
  ModelType
} from '@inventreedb/ui';
import { Stack, Table, Text, Title } from '@mantine/core';
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
  // Format numeric values to 3 decimal places
  const formatValue = (value: number | null | undefined) => {
    if (value === null || value === undefined) return 'n/a';
    return (value as number).toFixed(3);
  };

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
            <Text>
              Total Weight: {formatValue(apiQuery.data.total_weight)}{' '}
              {apiQuery.data.weight_unit}
            </Text>
            <Text>
              Total Volume: {formatValue(apiQuery.data.total_volume)}{' '}
              {apiQuery.data.volume_unit}
            </Text>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Part Name</Table.Th>
                  <Table.Th ta='right'>Qty</Table.Th>
                  <Table.Th ta='right'>
                    Weight/ea{' '}
                    {apiQuery.data.weight_unit
                      ? `(${apiQuery.data.weight_unit})`
                      : ''}
                  </Table.Th>
                  <Table.Th ta='right'>
                    Volume/ea{' '}
                    {apiQuery.data.volume_unit
                      ? `(${apiQuery.data.volume_unit})`
                      : ''}
                  </Table.Th>
                  <Table.Th ta='right'>
                    Line Weight{' '}
                    {apiQuery.data.weight_unit
                      ? `(${apiQuery.data.weight_unit})`
                      : ''}
                  </Table.Th>
                  <Table.Th ta='right'>
                    Line Volume{' '}
                    {apiQuery.data.volume_unit
                      ? `(${apiQuery.data.volume_unit})`
                      : ''}
                  </Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {apiQuery.data.parts.map((p: any) => (
                  <Table.Tr key={p.part_id}>
                    <Table.Td>{p.part_name ?? '–'}</Table.Td>
                    <Table.Td ta='right'>{formatValue(p.quantity)}</Table.Td>
                    <Table.Td ta='right'>{formatValue(p.weight)}</Table.Td>
                    <Table.Td ta='right'>{formatValue(p.volume)}</Table.Td>
                    <Table.Td ta='right'>{formatValue(p.line_weight)}</Table.Td>
                    <Table.Td ta='right'>{formatValue(p.line_volume)}</Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
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
