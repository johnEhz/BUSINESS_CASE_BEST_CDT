export interface LambdaProxyResponse<T = unknown> {
  statusCode: number;
  headers?: Record<string, string>;
  body: string;
  isBase64Encoded?: boolean;
  parsedBody?: T;
}