ExecutiveOrderDocument {
  metadata: Metadata,
  data: Data,
  content: Content
}

Metadata {
  saved_at: string,         // ISO datetime format
  last_updated: string      // ISO datetime format
}

Data {
  title: string,
  type: string,
  abstract: string | null,
  document_number: string,
  html_url: string,
  pdf_url: string,
  public_inspection_pdf_url: string,
  publication_date: string, // ISO date format
  agencies: Agency[],
  excerpts: any | null      // may contain additional excerpts data or be null
}

Content {
  abstract: string | null,
  action: string | null,
  agencies: Agency[],
  body_html_url: string,
  cfr_references: any[],    // empty array expected if none
  citation: string,
  comment_url: string | null,
  comments_close_on: string | null,
  correction_of: string | null,
  corrections: any[],       // array of corrections if any
  dates: any | null,        // additional date info if available
  disposition_notes: string,
  docket_ids: any[],
  dockets: any[],
  document_number: string,
  effective_on: string | null,
  end_page: number,
  executive_order_notes: string,
  executive_order_number: string,
  explanation: string | null,
  full_text_xml_url: string,
  html_url: string,
  images: {                // image URL mapping by key (e.g., "TRUMP")
    [key: string]: {
      large: string,
      original_size: string
    }
  },
  images_metadata: {       // detailed image metadata mapping by key
    [key: string]: {
      large: ImageMetadata,
      original_size: ImageMetadata
    }
  },
  json_url: string,
  mods_url: string,
  not_received_for_publication: any | null,
  page_length: number,
  page_views: {
    count: number,
    last_updated: string     // ISO datetime format
  },
  pdf_url: string,
  presidential_document_number: string,
  proclamation_number: string | null,
  public_inspection_pdf_url: string,
  publication_date: string,   // ISO date format
  raw_text_url: string,
  regulation_id_number_info: object,
  regulation_id_numbers: any[],
  regulations_dot_gov_info: object,
  regulations_dot_gov_url: string | null,
  significant: any | null,
  signing_date: string,       // ISO date format
  start_page: number,
  subtype: string,
  title: string,
  toc_doc: string,
  toc_subject: string | null,
  topics: any[],              // topics list if available
  type: string,
  volume: number
}

Agency {
  raw_name: string,
  name: string,
  id: number,
  url: string,
  json_url: string,
  parent_id: number | null,
  slug: string
}

ImageMetadata {
  identifier: string,
  content_type: string,
  size: number,
  width: number,
  sha: string,
  url: string,
  height: number
}
