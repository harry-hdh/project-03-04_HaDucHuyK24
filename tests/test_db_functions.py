from unittest.mock import MagicMock, patch
from src.project_03.utils import fetch_sequence_name, resync_sequence


@patch('src.project_03.utils.create_cur')
def test_fetch_sequence_name_success(mock_create_cur):
    # Setup mock cursor and connection
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_create_cur.return_value = (mock_cur, mock_conn)

    # Simulate database returning a sequence name
    mock_cur.fetchone.return_value = ('products_product_id_seq',)

    result = fetch_sequence_name('products', 'product')

    # Assertions
    assert result == 'public.products_product_id_seq'
    mock_cur.execute.assert_called_once()
    # Verify the SQL being sent is what we expect
    assert "pg_get_serial_sequence" in mock_cur.execute.call_args[0][0]


@patch('src.project_03.utils.fetch_sequence_name')
@patch('src.project_03.utils.create_cur')
def test_resync_sequence_calls_commit(mock_create_cur, mock_fetch):
    # Setup mocks
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_create_cur.return_value = (mock_cur, mock_conn)
    mock_fetch.return_value = 'public.products_product_id_seq'

    resync_sequence('brands','brand_id')

    # Ensure commit was called (if it isn't, the DB won't update!)
    mock_conn.commit.assert_called_once()
    mock_cur.close.assert_called_once()